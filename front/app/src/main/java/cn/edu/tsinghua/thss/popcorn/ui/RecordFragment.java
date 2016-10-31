package cn.edu.tsinghua.thss.popcorn.ui;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import android.content.Context;
import android.widget.BaseAdapter;
import android.widget.TextView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.FontAwesomeText;
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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cn.edu.tsinghua.thss.popcorn.RecordListActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;


/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class RecordFragment extends ListFragment {
    static private int REQUEST_CODE = 2;
    String[] mTitle, mTime, mID, mInterval;
    RouteListAdapter adapter;
    private View recordView;

    public void updateRecord() {
            //接收消息后要做的处理
            SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String time = df.format(new Date());

            RequestParams params = new RequestParams();
            params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
            params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
            params.addQueryStringParameter("timestamp", time);

            HttpUtils http = new HttpUtils();
            http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
            http.send(HttpRequest.HttpMethod.GET,
                    Config.ROUTE_GET_URL,
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
                                ArrayList<String> tmp_title = new ArrayList<String>();
                                ArrayList<String> tmp_time = new ArrayList<String>();
                                ArrayList<String> tmp_route_id = new ArrayList<String>();
                                ArrayList<String> tmp_interval = new ArrayList<String>();
                                if (status.equals("ok")) {
                                    JSONArray results = jsonObject.getJSONArray("data");
                                    for (int i = 0; i < results.length(); ++i) {
                                        JSONObject result = results.getJSONObject(i);
                                        String name = result.getString("name");
                                        String str_start_time = result.getString("start_time");
                                        String route_id = result.getString("id");
                                        String str_interval = result.getString("interval");
                                        tmp_title.add(name);
                                        tmp_time.add(str_start_time);
                                        tmp_route_id.add(route_id);
                                        tmp_interval.add(str_interval);
                                    }
                                    mTitle = tmp_title.toArray(new String[]{});
                                    mTime = tmp_time.toArray(new String[]{});
                                    mID = tmp_route_id.toArray(new String[]{});
                                    mInterval = tmp_interval.toArray(new String[]{});
                                    setListAdapter(adapter);
                                } else {
                                    //Toast.makeText(getActivity(), "您今天没有抄表任务", Toast.LENGTH_SHORT).show();
                                    //bottomTabMeterText.setText(String.valueOf(1));
                                    //bottomTabMeterText.setText("2");
                                    //bottomTabMeterText.setTextSize(50);
                                    //bottomTabMeterText.setVisibility(View.GONE);
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        @Override
                        public void onFailure(HttpException error, String msg) {
                            //Toast.makeText(, "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                            NoRepeatToast.showToast(getActivity(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                        }
                    });
        }


	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
		//View recordView = inflater.inflate(R.layout.activity_tab_record, container,false);
        if(recordView==null){
            recordView=inflater.inflate(R.layout.activity_tab_record, null);
        }
        //缓存的rootView需要判断是否已经被加过parent， 如果有parent需要从parent删除，要不然会发生这个rootview已经有parent的错误。
        ViewGroup parent = (ViewGroup) recordView.getParent();
        if (parent != null) {
            parent.removeView(recordView);
        }

        adapter = new RouteListAdapter(getActivity());

        updateRecord();

        return recordView;
	}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public void setUserVisibleHint(boolean isVisibleToUser) {
        super.setUserVisibleHint(isVisibleToUser);
        if (isVisibleToUser) {
            updateRecord();
        } else {
            //相当于Fragment的onPause
        }
    }
    @Override
    public void onDestroy(){
        super.onDestroy();
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent = new Intent(getActivity(), RecordListActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("route_id", mID[(int)id]);
        intent.putExtras(bundle);
        //intent.putExtra("route_id",id);
        startActivityForResult(intent, REQUEST_CODE);

        super.onListItemClick(l, v, position, id);
    }

    @Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (Activity.RESULT_OK == resultCode && requestCode == REQUEST_CODE) {
            setListAdapter(adapter);
            //mAdapter.notifyDataSetChanged();
        }
    }

    private List<Map<String, Object>> getData(String[] str_title, String[] str_time, String[] str_interval) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_title.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("title", str_title[i]);
            map.put("start_time", str_time[i]);
            map.put("interval", str_interval[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView title;
        public TextView start_time;
        public TextView interval;
        public FontAwesomeText faText;
    }

    public class RouteListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RouteListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mTitle.length;
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_tab_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.start_time = (TextView) convertView.findViewById(R.id.start_time);
                holder.interval = (TextView) convertView.findViewById(R.id.interval);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText(mTitle[position]);
            holder.start_time.setText(mTime[position]);
            holder.interval.setText(mInterval[position] + "小时一次");

            return convertView;
        }
    }
}