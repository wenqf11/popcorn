package cn.edu.tsinghua.thss.popcorn;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ListView;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class DeviceInfoSearchActivity extends Activity implements
        SearchView.OnQueryTextListener{

    private SearchView searchView;
    private ArrayList<String> deviceBrief = new ArrayList<String>();;
    private HintAdapter adapter;

    @ViewInject(R.id.device_info_hint_listview)
    private ListView hintListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_info_search);

        ViewUtils.inject(this);

        initActionbar();
        initListViewandAapter();
    }

    private void initListViewandAapter(){
        loadData();
        adapter = new HintAdapter(this, deviceBrief);
        hintListView.setAdapter(adapter);
        hintListView.setTextFilterEnabled(true);
        searchView.setOnQueryTextListener(this);


        hintListView.setOnItemClickListener(new AdapterView.OnItemClickListener(){

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                //searchView.setQuery(adapter.getItem(position).toString(), true);
                Intent intent = new Intent(getApplicationContext(), DeviceInfoDetailActivity.class);
                Bundle bundle = new Bundle();
                bundle.putString("device_brief", deviceBrief.get(position));
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

    }

    private void initActionbar() {
        // 自定义标题栏
        getActionBar().setDisplayShowHomeEnabled(false);
        getActionBar().setDisplayShowTitleEnabled(false);
        getActionBar().setDisplayShowCustomEnabled(true);
        Drawable draw=this.getResources().getDrawable(R.drawable.actionbar_bg);
        getActionBar().setBackgroundDrawable(draw);

        LayoutInflater mInflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View mTitleView = mInflater.inflate(R.layout.custom_action_bar_layout, null);
        getActionBar().setCustomView(
                mTitleView,
                new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT,
                        ActionBar.LayoutParams.WRAP_CONTENT));
        searchView = (SearchView) mTitleView.findViewById(R.id.search_view);
    }

    public void loadData() {
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_ALL_DEVICE_BRIEF_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if (status.equals("ok")) {
                                JSONArray briefList = jsonObject.getJSONArray("data");
                                for(int i = 0; i<briefList.length(); i++){
                                    deviceBrief.add(briefList.getString(i));
                                }
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    public class HintAdapter extends BaseAdapter implements Filterable{

        private LayoutInflater mInflater = null;
        private HintHolder holder = null;
        public ArrayList<String> nameList = null;
        public ArrayList<String> originNameList = null;

        public HintAdapter(Context context, ArrayList<String> data) {
            super();
            this.nameList = data;
            this.originNameList = data;
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        public class HintHolder
        {
            TextView name;
        }

        @Override
        public int getCount() {
            // TODO Auto-generated method stub
            //return emp_list.size();
            if(nameList == null){
                return 0;
            }else{
                return nameList.size();
            }
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return nameList.get(position);
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public Filter getFilter() {
            return new Filter() {

                @Override
                protected FilterResults performFiltering(CharSequence constraint) {
                    final FilterResults oReturn = new FilterResults();
                    final ArrayList<String> results = new ArrayList<String>();

                    if (constraint != null) {
                        if (originNameList != null && originNameList.size() > 0) {
                            for (final String st : originNameList) {
                                if (st.toLowerCase()
                                        .contains(constraint.toString().toLowerCase()))
                                    results.add(st);
                            }
                        }
                        oReturn.values = results;
                    }
                    return oReturn;
                }

                @SuppressWarnings("unchecked")
                @Override
                protected void publishResults(CharSequence constraint,
                                              FilterResults results) {
                    nameList = (ArrayList<String>) results.values;
                    notifyDataSetChanged();
                }
            };
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            // TODO Auto-generated method stub

            if(convertView==null)
            {
                convertView=mInflater.inflate(R.layout.listview_search_hint, parent, false);
                holder = new HintHolder();
                holder.name=(TextView) convertView.findViewById(R.id.listview_search_hint_name);
                convertView.setTag(holder);
            }
            else
            {
                holder = (HintHolder) convertView.getTag();
            }

            holder.name.setText(nameList.get(position));

            return convertView;

        }

    }



    //用户输入字符时触发该方法
    @Override
    public boolean onQueryTextChange(String newText) {
        hintListView.setVisibility(View.VISIBLE);
        if (TextUtils.isEmpty(newText)) {
            HintAdapter ca = (HintAdapter)hintListView.getAdapter();
            ca.getFilter().filter("");
        } else {
            HintAdapter ca = (HintAdapter)hintListView.getAdapter();
            ca.getFilter().filter(newText);
        }
        return false;
    }

    //单击搜索按钮时触发该方法
    @Override
    public boolean onQueryTextSubmit(String query) {
        hintListView.setVisibility(View.GONE);
        return false;
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.device_info_search, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
