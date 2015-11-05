package cn.edu.tsinghua.thss.popcorn.ui;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.ContentResolver;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Calendar;

import cn.edu.tsinghua.thss.popcorn.MainActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.UserInfoActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class ReportFragment extends Fragment {
//    private static String ACCESS_TOKEN = "hello_world";
    private static final int TAKE_PICTURE = 1;
    private static final int BROWSE = 2;

    private ProgressDialog progressDialog;

    private View reportView;

    // 获取sd卡根目录地址,并创建图片父目录文件对象和文件的对象;
    String file_str = Environment.getExternalStorageDirectory().getPath();
    String file_path = file_str + "/willwings/photos";
    File mars_file = new File(file_path);
    File file_go = new File(file_path+"/origin.jpg");

    @ViewInject(R.id.tab_report_camera)
    private Button cameraButton;

    //@ViewInject(R.id.tab_report_browse)
  //  private Button browseButton;

    @ViewInject(R.id.tab_report_submit_btn)
    private Button submitButton;

    @ViewInject(R.id.tab_report_title)
    private EditText reportTitleText;

    @ViewInject(R.id.tab_report_device_brief)
    private EditText deviceBriefText;

    @ViewInject(R.id.tab_report_fault_description)
    private EditText faultDescriptionText;

    @ViewInject(R.id.tab_report_memo)
    private EditText reportMemoText;

    @ViewInject(R.id.tab_report_img)
    private ImageView image_view;

    @OnClick(R.id.tab_report_submit_btn)
    private void submitButtonClick(View v){
        String deviceBrief = deviceBriefText.getText().toString();
        final String reportTitle = reportTitleText.getText().toString();
        String faultDescription = faultDescriptionText.getText().toString();
        String reportMemo = reportMemoText.getText().toString();

        if(reportTitle.equals("")){
            new AlertDialog.Builder(getActivity())
                    .setTitle("报修标题不能为空！")
                    .setPositiveButton("确定",null)
                    .show();
            return ;
        }

        if(faultDescription.equals("")){
            new AlertDialog.Builder(getActivity())
                    .setTitle("故障描述不能为空！")
                    .setPositiveButton("确定",null)
                    .show();
            return ;
        }

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("device_brief", deviceBrief);
        params.addBodyParameter("title", reportTitle);
        params.addBodyParameter("description", faultDescription);
        params.addBodyParameter("memo", reportMemo);

        progressDialog.setMessage("数据发送中...");
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.REPORT_URL,
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
                        progressDialog.hide();

                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if (status.equals("ok")) {
                                String repairTaskId = jsonObject.getString("data");
                                if(image_view.getDrawable() != null){
                                    RequestParams params = new RequestParams();
                                    params.addBodyParameter("username", Config.DEBUG_USERNAME);
                                    params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                                    params.addBodyParameter("id", repairTaskId);
                                    params.addBodyParameter("image", new File(Config.REPORT_FILE_PATH));

                                    HttpUtils http = new HttpUtils();
                                    http.send(HttpRequest.HttpMethod.POST,
                                            Config.SUBMIT_REPORT_IMAGE_URL,
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
                                                    Toast.makeText(getActivity().getApplicationContext(), "报修成功", Toast.LENGTH_SHORT).show();
                                                    reportTitleText.setText("");
                                                    deviceBriefText.setText("");
                                                    faultDescriptionText.setText("");
                                                    reportMemoText.setText("");
                                                    image_view.setImageBitmap(null);
                                                }

                                                @Override
                                                public void onFailure(HttpException error, String msg) {
                                                }
                                            }
                                    );
                                }else{
                                    Toast.makeText(getActivity().getApplicationContext(), "报修成功", Toast.LENGTH_SHORT).show();
                                    reportTitleText.setText("");
                                    deviceBriefText.setText("");
                                    faultDescriptionText.setText("");
                                    reportMemoText.setText("");
                                }
                            } else {
                                Toast.makeText(getActivity().getApplicationContext(), "数据提交失败，请重试", Toast.LENGTH_SHORT).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }

                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getActivity().getApplicationContext(), "数据提交失败，请重试", Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }

    @OnClick(R.id.tab_report_camera)
    private void cameraButtonClick(View v){
        if (Environment.MEDIA_MOUNTED.equals(Environment
                .getExternalStorageState())) {
            // 先创建父目录，如果新创建一个文件的时候，父目录没有存在，那么必须先创建父目录，再新建文件。
            if (!mars_file.exists()) {
                mars_file.mkdirs();
            }
            // 设置跳转的系统拍照的activity为：MediaStore.ACTION_IMAGE_CAPTURE ;
            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file_go));
            //跳转到拍照界面;
            startActivityForResult(intent, TAKE_PICTURE);
        } else {
            Toast.makeText(getActivity(), "请先安装好SD卡",Toast.LENGTH_LONG).show();
        }
    }

   /* @OnClick(R.id.tab_report_browse)
    private void browseButtonClick(View v){
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent, BROWSE);
    }*/

	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
//        if (reportView != null)
//            return reportView;
//
//		reportView = inflater.inflate(R.layout.activity_tab_report, container,false);
        if(reportView==null){
            reportView=inflater.inflate(R.layout.activity_tab_report, null);
        }
        //缓存的rootView需要判断是否已经被加过parent， 如果有parent需要从parent删除，要不然会发生这个rootview已经有parent的错误。
        ViewGroup parent = (ViewGroup) reportView.getParent();
        if (parent != null) {
            parent.removeView(reportView);
        }
        //return reportView;

        ViewUtils.inject(this, reportView);
        progressDialog = new ProgressDialog(getActivity(), R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(true);

        return reportView;
	}


    //拍照结束后显示图片;
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        // 判断请求码和结果码是否正确，如果正确的话就显示刚刚所拍照的图片;
        if (resultCode == getActivity().RESULT_OK){
            if(requestCode == TAKE_PICTURE){
                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize = 2;
                Bitmap bmpDefaultPic = BitmapFactory.decodeFile(file_go.getPath(), options);
                image_view.setImageBitmap(bmpDefaultPic);
                saveBitmap(bmpDefaultPic, Config.REPORT_FILE_PATH);
            }else if(requestCode == BROWSE) {
                Uri uri = data.getData();
                ContentResolver cr = getActivity().getContentResolver();
                try {
                    Bitmap bitmap = BitmapFactory.decodeStream(cr.openInputStream(uri));
                    image_view.setImageBitmap(bitmap);
                    saveBitmap(bitmap, Config.REPORT_FILE_PATH);
                } catch (FileNotFoundException e) {
                    Log.e("Exception", e.getMessage(),e);
                }
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private void saveBitmap(Bitmap bm, String path) {
        File f = new File(path);
        try {
            FileOutputStream out = new FileOutputStream(f);
            bm.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }
	
	@Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}
}
